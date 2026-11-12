from streamlit import *
title("10주차 스트림릿")

info("스트림릿입니다. 10주차 수업입니다.") #파란색
error("에러 연습") #빨간색
success("성공 연습") #초록색
warning("경고 연습") #노란색

header("헤더 연습") #메인제목
subheader("서브헤더 연습") #중제목
markdown("마크다운 연습") #마크다운
write("write 연습. 그냥 뭐든 쓰는 식으로") #write

code("print(\"Hello, World!\")")

write("---") #구분선
image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT3rSZ71LJ9xq4A3fRHtBnMObbJhi2wMyyADc-TaQ4eWA&s=10", caption="매익불슷도리") #이미지
video("https://www.youtube.com/watch?v=jUE74BveuIE&list=RDjUE74BveuIE&start_radio=1")
link_button("desmos 버튼", "https://www.naver.com") #링크 버튼
write("---")