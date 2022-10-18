function openStudyTimer() {
    localStorage.setItem('popup', 'true');
    if (!window.open('/study/timer', 'Study Timer', 'width=500,height=450,left=100,top=100'))
        window.open("/study/timer", "_blank");
}