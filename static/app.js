async function updateContent() { //value is the companyname
    const form1 = document.getElementById('passwordForm');
            while (form1.lastChild) {
                form1.removeChild(form1.lastChild);
            };


    let value = document.getElementById('userInput').value;
    const companyname = document.createElement('input');
    companyname.setAttribute("id", 'companyname')
    companyname.setAttribute('name', 'companyname');
    companyname.setAttribute('hidden', true);
    companyname.setAttribute('type', 'text');
    companyname.setAttribute('maxlength', '50');
    companyname.setAttribute('value', value);

    form1.append(companyname);


    let reply = await fetch("/getdata?data=" + value);
    if (reply.status == 200) {
        // console.log(reply)
        console.log(reply);
        if (reply.redirected == true){
            window.location.href = reply.url;
        };

        let result = await reply.json();
        console.log("RESULT: ", result)

        if(result.length >= 1){
            
            for(let i = 0; i < result.length; i++){
                datarow = result[i].split(";"); //datarow = [stotteordning, brukernavn, passord]
                console.log("DATAROW: ", datarow);
                let stotteordning = datarow[0];
                let username1 = datarow[1];
                let password = datarow[2];

                // THE FOLLOWING CODE CREATES A NEW INPUT SECTION FOR A STØTTEORDNING, THIS INCLUDES PASSWORDS
                // First, select the element where you want to append the new elements
                const form = document.getElementById('passwordForm');

                // Create the <h4> element and set its content
                const h4 = document.createElement('h4');
                h4.textContent = stotteordning + ":";
                form.appendChild(h4);

                //Hidden input containing the støtteordning name, it is called stotteord
                const stotteordinput = document.createElement('input');
                stotteordinput.setAttribute('id', 'stotteord' + i);
                stotteordinput.setAttribute('name', 'stotteord' + i);
                stotteordinput.setAttribute('hidden', true);
                stotteordinput.setAttribute('type', 'text');
                stotteordinput.setAttribute('maxlength', '50');
                stotteordinput.setAttribute('value', stotteordning);
                //stotteordinput.textContent = stotteordning;
                form.appendChild(stotteordinput);

                // Create the first div for the username input group
                const divUsernameGroup = document.createElement('div');
                divUsernameGroup.setAttribute('class', 'input-group');

                // username label
                const labelUsername = document.createElement('label');
                labelUsername.setAttribute('for', 'username' + i);
                labelUsername.textContent = 'Brukernavn:';

                // username input
                const inputUsername = document.createElement('input');
                inputUsername.setAttribute('id', 'username' + i);
                inputUsername.setAttribute('name', 'username'+i);
                inputUsername.setAttribute('class', 'output');
                inputUsername.setAttribute('type', 'text');
                inputUsername.setAttribute('maxlength', '50');
                inputUsername.setAttribute('value', username1);
                //inputUsername.textContent = username1;

                // username copy button
                const buttonCopyUsername = document.createElement('button');
                buttonCopyUsername.setAttribute('type', 'button');
                let copytoclip = "copyToClipboard('username" + i + "')"
                buttonCopyUsername.setAttribute('onclick', copytoclip);
                buttonCopyUsername.textContent = 'Kopier';

                // Append label, input, and button to the div
                divUsernameGroup.appendChild(labelUsername);
                divUsernameGroup.appendChild(inputUsername);
                divUsernameGroup.appendChild(buttonCopyUsername);

                // Append the div to the form
                form.appendChild(divUsernameGroup);

                // Create the second div for the password input group
                const divPasswordGroup = document.createElement('div');
                divPasswordGroup.setAttribute('class', 'input-group');

                // password label
                const labelPassword = document.createElement('label');
                labelPassword.setAttribute('for', 'pass'+i);
                labelPassword.textContent = 'Passord:';

                // password input
                const inputPassword = document.createElement('input');
                inputPassword.setAttribute('id', 'pass'+i);
                inputPassword.setAttribute('name', 'pass'+i);
                inputPassword.setAttribute('class', 'output');
                inputPassword.setAttribute('type', 'password');
                inputPassword.setAttribute('maxlength', '50');
                inputPassword.setAttribute('value', password);
                //inputPassword.textContent = password;

                // password copy button
                const buttonCopyPassword = document.createElement('button');
                buttonCopyPassword.setAttribute('type', 'button');
                let copytoclip2 = "copyToClipboard('pass" + i + "')"
                buttonCopyPassword.setAttribute('onclick', copytoclip2);
                buttonCopyPassword.textContent = 'Kopier';

                // Append label, input, and button to the div
                divPasswordGroup.appendChild(labelPassword);
                divPasswordGroup.appendChild(inputPassword);
                divPasswordGroup.appendChild(buttonCopyPassword);

                // Append the div to the form
                form.appendChild(divPasswordGroup);

            };

            // getting the form element for appending the update info button
            const form2 = document.getElementById('passwordForm');

            // creating update info button
            const updatebutton1 = document.createElement('button');
            updatebutton1.setAttribute('id', 'updatebutton');
            updatebutton1.setAttribute('type', 'submit');
            updatebutton1.setAttribute('class', 'submit-btn');
            updatebutton1.setAttribute('onclick', 'oppdaterPassord()');
            updatebutton1.textContent = 'Oppdater informasjon';


            // append back the update info button
            form2.appendChild(updatebutton1);

            console.log(form2.children.length);
        };
    }  
}


function legg_til_ny_bedrift() {
    const form1 = document.getElementById('passwordForm');
            while (form1.lastChild) {
                form1.removeChild(form1.lastChild);
            };

            const form = document.getElementById('passwordForm');

                // Create the <h4> element and set its content
                const h4 = document.createElement('h4');
                h4.textContent = "Legg til en ny støtteordning eller bedrift:";
                form.appendChild(h4);

                // lager en div for selskapsnavn
                const divnavnGroup = document.createElement('div');
                divnavnGroup.setAttribute('class', 'input-group');

                const labelnavn = document.createElement('label');
                labelnavn.setAttribute('for', 'navn');
                labelnavn.textContent = 'Selskapsnavn:';

                //Hidden input containing the Selskapsnavn name, it is called stotteord
                const navninput = document.createElement('input');
                navninput.setAttribute('id', 'navn');
                navninput.setAttribute('class', 'output');
                navninput.setAttribute('name', 'navn');
                navninput.setAttribute('type', 'text');
                navninput.setAttribute('maxlength', '50');

                divnavnGroup.appendChild(labelnavn);
                divnavnGroup.appendChild(navninput);

                form.appendChild(divnavnGroup);


                // lager en div for organisasjonsnummer
                const divorgnrGroup = document.createElement('div');
                divorgnrGroup.setAttribute('class', 'input-group');

                const labelorgnr = document.createElement('label');
                labelorgnr.setAttribute('for', 'orgnr');
                labelorgnr.textContent = 'Org. nummer:';

                //Hidden input containing the støtteordning name, it is called stotteord
                const orgnrinput = document.createElement('input');
                orgnrinput.setAttribute('id', 'orgnr');
                orgnrinput.setAttribute('class', 'output');
                orgnrinput.setAttribute('name', 'orgnr');
                orgnrinput.setAttribute('type', 'text');
                orgnrinput.setAttribute('maxlength', '50');

                divorgnrGroup.appendChild(labelorgnr);
                divorgnrGroup.appendChild(orgnrinput);

                form.appendChild(divorgnrGroup);


                // Create the div for the stotteordning input group
                const divstotteordGroup = document.createElement('div');
                divstotteordGroup.setAttribute('class', 'input-group');

                const labelstotteord = document.createElement('label');
                labelstotteord.setAttribute('for', 'stotteord');
                labelstotteord.textContent = 'Støtteordning:';

                //Hidden input containing the støtteordning name, it is called stotteord
                const stotteordinput = document.createElement('input');
                stotteordinput.setAttribute('id', 'stotteord');
                stotteordinput.setAttribute('class', 'output');
                stotteordinput.setAttribute('name', 'stotteord');
                stotteordinput.setAttribute('type', 'text');
                stotteordinput.setAttribute('maxlength', '50');

                divstotteordGroup.appendChild(labelstotteord);
                divstotteordGroup.appendChild(stotteordinput);

                form.appendChild(divstotteordGroup);

                // Create the first div for the username input group
                const divUsernameGroup = document.createElement('div');
                divUsernameGroup.setAttribute('class', 'input-group');

                // username label
                const labelUsername = document.createElement('label');
                labelUsername.setAttribute('for', 'username');
                labelUsername.textContent = 'Brukernavn:';

                // username input
                const inputUsername = document.createElement('input');
                inputUsername.setAttribute('id', 'username');
                inputUsername.setAttribute('name', 'username');
                inputUsername.setAttribute('class', 'output');
                inputUsername.setAttribute('type', 'text');
                inputUsername.setAttribute('maxlength', '50');

                // Append label, input, and button to the div
                divUsernameGroup.appendChild(labelUsername);
                divUsernameGroup.appendChild(inputUsername);

                // Append the div to the form
                form.appendChild(divUsernameGroup);

                // Create the second div for the password input group
                const divPasswordGroup = document.createElement('div');
                divPasswordGroup.setAttribute('class', 'input-group');

                // password label
                const labelPassword = document.createElement('label');
                labelPassword.setAttribute('for', 'pass');
                labelPassword.textContent = 'Passord:';

                // password input
                const inputPassword = document.createElement('input');
                inputPassword.setAttribute('id', 'pass');
                inputPassword.setAttribute('name', 'pass');
                inputPassword.setAttribute('class', 'output');
                inputPassword.setAttribute('type', 'password');
                inputPassword.setAttribute('maxlength', '50');

                // Append label, input, and button to the div
                divPasswordGroup.appendChild(labelPassword);
                divPasswordGroup.appendChild(inputPassword);

                // Append the div to the form
                form.appendChild(divPasswordGroup);


                // password input
                const inputSubmit = document.createElement('input');
                inputSubmit.setAttribute('id', 'addbutton');
                inputSubmit.setAttribute('class', 'submit-btn');
                inputSubmit.setAttribute('type', 'submit');
                inputSubmit.textContent = "Legg til";

                // Append label, input, and button to the div
                divPasswordGroup.appendChild(inputSubmit);

                // Append the div to the form
                form.appendChild(inputSubmit);
                form.setAttribute('action', '/addnewinfo')
                
}




function oppdaterPassord() {
    alert("Takk! Informasjonen er oppdatert.")
}

function copyToClipboard(datatype) {
    console.log(datatype)
    var copyText = document.getElementById(datatype); //datatype is either "username" or "pass" or "username1" or "pass1" etc.

    // Select the text field
    copyText.select();
    copyText.setSelectionRange(0, 99999); // For mobile devices

    // Copy the text inside the text field
    navigator.clipboard.writeText(copyText.value);
}