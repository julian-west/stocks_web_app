// Change colour of positive and negative numbers

function waitForElm(selector) {
    return new Promise(resolve => {
        if (document.querySelector(selector)) {
            return resolve(document.querySelector(selector));
        }

        const observer = new MutationObserver(mutations => {
            if (document.querySelector(selector)) {
                resolve(document.querySelector(selector));
                observer.disconnect();
            }
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    });
}

waitForElm('.number').then((elm) => {
    var elements = document.getElementsByClassName("number")

    for (i = 0; i < elements.length; i++) {
        num = elements[i].textContent.slice(0, -1)

        if (num > 0) {
            elements[i].style.color = "green"
            elements[i].textContent = "+" + elements[i].textContent
        } else {
            elements[i].style.color = "red"
        }
    }
});
