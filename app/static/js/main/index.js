window.onload = function () {
    if (localStorage.getItem('color-theme') === 'dark') {
        let daelements = document.getElementsByClassName('changeable-gradient');
        console.log(daelements);
        for (let element of daelements) {
            element.classList.remove('gradient-text');
            element.classList.add('gradient-text-dark');
        }
    }
};
