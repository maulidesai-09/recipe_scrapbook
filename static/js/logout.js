// JS for logout confirmation

const logout = document.querySelector("#logout");

logout.addEventListener('click', (evt) => {
    evt.preventDefault();

    const user_id = document.querySelector("#user_id_navbar").innerHTML
    let confirmation = null

    if (confirm("Are you sure you want to logout") === true) {
        confirmation = "Yes";
    } else {
        confirmation = "No";
    }

    // const url= `/logout?confirmation=${confirmation}`

    const url= `/login/${user_id}/logout?confirmation=${confirmation}`

    window.location.href = url
})