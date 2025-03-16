//select the navbar
const dropdownContainers = document.querySelectorAll('.dropdown');
console.log(dropdownContainers);
const navItems = document.querySelectorAll('.nav-item');

const show = function(event){
    let dropdown = this.nextElementSibling;
    console.log('showing...', dropdown);
    dropdown.style.display = 'block';
    setTimeout(()=>{
        dropdown.style.opacity = 1; //make visible
        dropdown.style.transform = 'translateY(0)';
    },10);
}

const hideDropdown = function(event){
    let dropdown = this.querySelector('.dropdown-content');

    console.log('hiding...');
    setTimeout(()=>{
        dropdown.style.opacity = 0;
        dropdown.style.transform = 'translateY(10px)';
    }, 300);
}

navItems.forEach((item)=>{
    console.log('adding listener to ', item)
    item.addEventListener('mouseover', show);
})

dropdownContainers.forEach((dropdownDiv)=>{
    dropdownDiv.addEventListener('mouseleave', hideDropdown);
})

