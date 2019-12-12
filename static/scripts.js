function logout(){
    window.location='/logout';
}

function validateRating(){
    rating_val = $('#rating_val').val()

    if ((rating_val <= 5) && (rating_val >= 1)){
        alert('Rating updated!')
    } else {
        alert('Invalid rating. Integer values from 1 to 5 only.')
    }
}

function invalidLogin(){
    alert('Invalid login, please try again.');
}