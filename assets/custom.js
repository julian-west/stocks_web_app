// Change colour of positive and negative numbers


document.addEventListener('DOMContentLoaded', function () {
    setTimeout(function () {
        var elements = document.getElementsByClassName("number")
        console.log(elements)

        for (i = 0; i < elements.length; i++) {
            num = elements[i].textContent.slice(0, -1)

            if (num > 0) {
                elements[i].style.color = "green"
                elements[i].textContent = "+" + elements[i].textContent
            } else {
                elements[i].style.color = "red"
            }
        }
    }, 5000)
}, false);

// var elements = document.getElementsByClassName("number")
// console.log(elements)

// for (i = 0; i < elements.length; i++) {
//     num = elements[i].textContent.slice(0, -1)

//     if (num > 0) {
//         elements[i].style.color = "green"
//         elements[i].textContent = "+" + elements[i].textContent
//     } else {
//         elements[i].style.color = "red"
//     }
// }
// alert('If you see this alert, then your custom JavaScript script has run!')
//     }, false)


