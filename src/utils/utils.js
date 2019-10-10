var triggerEvent = true;

function jsInit() {
    window.onscroll = function (event) {
        console.log(document.documentElement.scrollTop);
        if (triggerEvent) {

            // $$scrollTop
            py_get_coordinates(document.documentElement.scrollTop);
        }
    };
}

function py_scrollTo(position) {
    window.scroll(0, position);
    triggerEvent = false;

    setTimeout(() => {
        triggerEvent = true;
    }, 500);
}