from streamlit import *

title("수업 입장")
caption("코드를 입력하면 다음 내용이 열립니다.")

classcode = "12"

# 입력 칸을 가운데에 두기
left, center, right = columns([1, 2, 1])
with center:
    pw = text_input(
        "입장 코드",
        placeholder="여기에 코드를 입력하세요",
    )

code_text = pw.strip()

# 비었으면 안내, 맞으면 성공, 다르면 오류
if code_text == "":
    info("코드를 입력해 주세요.")
elif code_text == classcode:
    success("코드가 맞습니다. 입장되었습니다.")
    write("---")
    header("환영합니다")
    markdown("이제 이 페이지의 내용을 이어서 볼 수 있습니다.")
    
    subheader("다양한 input 예제 확인")
    image("problem.jpeg")

    write("위의 문제의 답을 입력해주세요.")

    # value=None이면 처음에 0이 아니라 빈 칸. 입력 전에는 None이 된다.
    ans = number_input(
        "답",
        min_value=0,
        max_value=999,
        value=None,
        step=1,
        format="%d",
        placeholder="정수만 입력 가능",
        key="ans",
    )

    if ans is None:
        info("답을 입력해 주세요.")
    elif ans == 624:
        success("정답입니다.")
    else:
        error("틀렸습니다. 다시 문제를 풀어주세요.")

    # 버튼을 누르면 위젯에 기억된 값을 비우고 다시 그린다.
    def clear_ans():
        session_state.ans = None

    button("다시 풀기", on_click=clear_ans)
        
else:
    error("코드가 틀렸습니다. 다시 확인해 주세요.")

