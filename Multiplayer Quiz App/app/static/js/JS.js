const toggleButton = document.getElementsByClassName('toggle-button')[0]
const navLinks = document.getElementsByClassName('nav-links')[0]

toggleButton.addEventListener('click', () => {
    navLinks.classList.toggle('active')
})

function show(){
	var pw = document.getElementByID('pw')
	var icon = document.querySelector('.fa')
	if (pw.type==="password"){
		pw.type = "text";
		pw.style.marginTop = "25px";
		icon.style.color = "#000"
	}else{
		pw.type = "password";
		icon.style.color = "grey"
	}
}