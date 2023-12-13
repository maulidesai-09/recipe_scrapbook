// JS for saving ingredients and instructions


const button_add_recipe = document.querySelector(".save_recipe_submit")

button_add_recipe.addEventListener("click", (evt) => {
    evt.preventDefault()

    const recipe_date = document.querySelector("#recipe_date").value
    const recipe_name = document.querySelector("#recipe_name").value
    const servings = document.querySelector("#servings").value
    const notes = document.querySelector("#notes").value
    const privacy = document.querySelector("input[name=privacy_radio]:checked").value

    // Getting ingredient details from HTML and preparing Object(dictionary) to be sent to server
    const ingredient_details = document.querySelectorAll(".ingredient_individual")
    const ingredients_list = []

    for (const ingredient_detail of ingredient_details) {
        let ingredient_obj = {}

        ingredient_obj['name'] = ingredient_detail.querySelector(".ingredient_name").value
        ingredient_obj['quantity'] = ingredient_detail.querySelector(".ingredient_quantity").value
        ingredient_obj['unit'] = ingredient_detail.querySelector(".ingredient_unit").value

        ingredients_list.push(ingredient_obj)
        // console.log(ingredient_detail)
    }


    // Getting instruction details from HTML and preparing Object(dictionary) (POST body known as 
    // 'Payload') to be sent to server
    const instruction_descriptions = document.querySelectorAll(".instruction_individual")
    const instructions_list = []

    for (const instruction_description of instruction_descriptions) {
        let instruction_obj = {}

        instruction_obj['description'] = instruction_description.querySelector(".instruction_description").value
        
        instructions_list.push(instruction_obj)
    }

    const recipe_id = document.querySelector("#recipe_id").innerHTML.trim()

    const recipe_data = {"recipe_id": recipe_id,
                        "recipe_date": recipe_date,
                        "recipe_name": recipe_name,
                        "servings": servings,
                        "notes": notes,
                        "privacy": privacy,
                        "ingredients": ingredients_list, 
                        "instructions": instructions_list}

    const user_id = document.querySelector("#user_id").innerHTML.trim()


    fetch("/login/"+user_id+"/new_recipe/add_recipe", {
        method: "POST",
        body: JSON.stringify(recipe_data),
        headers: {
            "Content-Type": "application/json",
        },
    })
    .then((response) => response.json())
    .then((responseJson) => {
        window.location.href  =`/login/${user_id}/saved_recipe/${responseJson}`;
    });
});





