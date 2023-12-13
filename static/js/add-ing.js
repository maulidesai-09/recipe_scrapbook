// JS to add new empty line for ingredients


const button = document.querySelector(".add_ingredient")

button.addEventListener("click", (evt) => {
    evt.preventDefault();

    // document.querySelector(".add_ingredient").remove();
    document.querySelector(".ingredient_details").insertAdjacentHTML('beforeend',
    `<div class="ingredient_individual">
    Ingredient Name
    <input type="text" name="ingredient_name" class="ingredient_name">
    Quantity
    <input type="text" name="ingredient_quantity" class="ingredient_quantity">
    Units
    <select  name="ingredient_unit" class="ingredient_unit">
        <option value="cup(s)"> cup </option>
        <option value="grams"> gram </option>
        <option value="ml"> ml </option>
        <option value="liter"> liter </option>
        <option value="oz"> oz </option>
        <option value="teaspoon"> teaspoon </option>
        <option value="tablespoon"> tablespoon </option>
        <option value="number"> number </option>
    </select>

    </div>`)

    // Move the 'Add' button for adding instructions to the latest ingredients line
    document.querySelector(".ingredient_individual:last-child").appendChild(document.querySelector(".add_ingredient"));



    
})



