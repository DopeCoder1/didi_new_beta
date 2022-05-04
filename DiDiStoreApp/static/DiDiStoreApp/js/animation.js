let search_line = document.querySelector('.search_line');
let search_icon = document.getElementById('search_icon');
let search_form = document.querySelector('.search_form');
search_icon.addEventListener('click', ()=>{
    search_line.classList.toggle('search_line_open');
    search_form.classList.toggle('search_form_animation');
});


document.addEventListener('click', (e)=>{
    let id = e.target.dataset.toggleId;
    if(id == "categories" || id == "registrations"){
        let overlay = document.getElementById('overlay');
        overlay.hidden = !overlay.hidden;
    }
    document.body.classList.toggle('scroll');
    let background = document.getElementById(id);
    background.hidden = !background.hidden; 
   
})
  

let sign_up = document.querySelector('.sign_up');
let sign_in = document.querySelector('.sign_in');
let registration_window = document.querySelector('.registration_window');
let sign_up_btn = document.getElementById('#sign_up').addEventListener('click',()=>{
    registration_window.classList.remove('registration_window_sign_in')
    sign_in.style.display = 'none';
    sign_up.style.display = 'block';
});
let sign_in_btn = document.getElementById('#sign_in').addEventListener('click',()=>{
    registration_window.classList.add('registration_window_sign_in')
    sign_in.style.display = 'block';
    sign_up.style.display = 'none';
});



