// JS to add new empty line for instructions

const button_instuction = document.querySelector(".add_instruction")

button_instuction.addEventListener("click", (evt) => {
    evt.preventDefault();

    document.querySelector(".instruction_details").insertAdjacentHTML('beforeend', 
    `<div class="instruction_individual">
    <textarea name="instructions" class="instruction_description" wrap="hard" style="width: 640px; height: 18px;"> </textarea>
    
    </div>`)

    // Move the 'Add' button for adding instructions to the latest instruction line
    document.querySelector(".instruction_individual:last-child").appendChild(document.querySelector(".add_instruction"));
})