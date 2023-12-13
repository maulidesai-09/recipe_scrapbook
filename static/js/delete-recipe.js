// JS for delete recipe confirmation

const delete_recipe_all = document.querySelectorAll(".delete_recipe");

for (const recipe of delete_recipe_all) {
    recipe.addEventListener('click', (evt) => {
        evt.preventDefault();

        const button = evt.target

        
        const user_id = document.querySelector(".user_id_del_recipe").innerHTML.trim()
        // const recipe_id = document.querySelector(".recipe_id_del_recipe").innerHTML.trim()
        const recipe_id = button.getAttribute("data-recipe-id")

        let confirmation = null

        if (confirm("Are you sure you want to delete this recipe") === true) {
            confirmation = "Yes";
        } else {
            confirmation = "No";
        }

        // const url= `/logout?confirmation=${confirmation}`

        const url = `/login/${user_id}/${recipe_id}/delete_recipe?confirmation=${confirmation}`

        window.location.href = url
    })

}