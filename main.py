import streamlit as st
import json
import requests

st.set_page_config(page_title="Streamlit Emojis", page_icon=":hotsprings:", layout="wide")
st.write("## Streamlit Emojis")
st.html("""
    <style>

        /* header的样式 */
        [data-testid="stHeader"] {
            height: 1px;
        }
        /* body的样式 */
        [data-testid="stAppViewBlockContainer"] { 
            padding: 20px 50px;
        }
        /* emojis 的样式 */
        .st-emotion-cache-eqffof > p {
        font-size: 1.5em;;
        }
    </style>

    """)

# 清空搜索框内容的函数
def clear_search():
    st.session_state.search = ''

def main():
    # 设置搜索行
    row_input = st.columns([4,1,1,13])
    # 添加文本输入框
    search_text = row_input[0].text_input('输入关键词以过滤图标:', key='search')
    # 添加搜索按钮
    row_input[1].text(" ")
    row_input[1].text(" ")
    search_button = row_input[1].button('搜索')
    # 添加清空按钮
    row_input[2].text(" ")
    row_input[2].text(" ")
    clear_button = row_input[2].button('清空',on_click = clear_search)

    try:
        with open("emoji.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as decode_error:
        st.error(f"Error decoding JSON: {decode_error}")
    except FileNotFoundError as fnf_error:
        st.error(f"File not found: {fnf_error}")
        # 使用加载的数据
        url = 'https://raw.githubusercontent.com/omnidan/node-emoji/master/lib/emoji.json'
        response = requests.get(url)
        data = json.loads(response.text)
        

    # 过滤数据
    if search_text:
        filtered_data = {k: v for k, v in data.items() if st.session_state.search.lower() in k.lower()}
    else:
        filtered_data = data    

    total = len(filtered_data)
    st.write(f"共 {total} 个图标")
    # st.write("---")
    # 多列网格显示全部emoji及其名称
    
    # 设置列数
    col_num = 4
    cols = st.columns(col_num)
    index = 0  # 添加索引计数器
    for name, emoji_char in filtered_data.items():
        # 确保同时输出emoji及其名称，前后加上 :
        cols[index % col_num].markdown(f"{emoji_char} :**{name}**:")
        # cols[index % col_num].markdown(f":**{name}**:")
        if index % col_num == col_num-1:  # 每指定的列数后换列
            cols = st.columns(col_num)
            # st.write("---")  # 每指定的列数后添加分割线
        index += 1


if __name__ == "__main__":
    main()