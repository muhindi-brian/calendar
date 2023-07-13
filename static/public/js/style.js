// set frontend time zone to selection
let zone = Intl.DateTimeFormat().resolvedOptions().timeZone
$(document).ready(function(){
    $('#timezone option:selected').text(zone)
    $('#timezone option:selected').val(zone)
})

// buttons
$(document).ready(function () {
    // toggle buttons functionality

    // display next event slots
    $("#next1").click(function () {
        $(".first").addClass('d-none');
        $(".second").removeClass('d-none');
        $("#next1").addClass('d-none');
        $("#next2").removeClass('d-none');
        $("#prev1").addClass('d-none');
        $("#prev2").removeClass('d-none');
    });

    $("#next2").click(function () {
        $(".second").addClass('d-none');
        $(".third").removeClass('d-none');
        $("#next2").addClass('d-none');
        $("#next3").removeClass('d-none');
        $("#prev2").addClass('d-none');
        $("#prev3").removeClass('d-none');
    });

    $("#next3").click(function () {
        $(".third").addClass('d-none');
        $(".fourth").removeClass('d-none');
        $("#next3").addClass('d-none');
        $("#next4").removeClass('d-none');
        $("#prev3").addClass('d-none');
        $("#prev4").removeClass('d-none');
    });

    // display previous event slots
    $("#prev2").click(function () {
        $(".first").removeClass('d-none');
        $(".second").addClass('d-none');
        $("#next1").removeClass('d-none');
        $("#next2").addClass('d-none');
        $("#prev1").removeClass('d-none');
        $("#prev2").addClass('d-none');
    });

    $("#prev3").click(function () {
        $(".second").removeClass('d-none');
        $(".third").addClass('d-none');
        $("#next2").removeClass('d-none');
        $("#next3").addClass('d-none');
        $("#prev2").removeClass('d-none');
        $("#prev3").addClass('d-none');
    });

    $("#prev4").click(function () {
        $(".third").removeClass('d-none');
        $(".fourth").addClass('d-none');
        $("#next3").removeClass('d-none');
        $("#next4").addClass('d-none');
        $("#prev3").removeClass('d-none');
        $("#prev4").addClass('d-none');
    });

    // Change slot bg
    $(".btn-grey").click(function() {
        // fix change in color on double clicking button
        $('.btn.text_grey.mb-3').css({'background-color': '#f2f2f2'});
        $(this).css({'background-color': '#ae2427'});
        // $(this).removeClass('btn-grey');
        // $('.btn.text_grey.mb-3.bg-maroon').addClass('btn-grey');
        // $('.btn.text_grey.mb-3.bg-maroon.btn-grey').removeClass('bg-maroon');
        // $(this).addClass('bg-maroon');
    });
});


// Display time
function updateTime() {
    $('#hour').html(new Date().getHours());
    $('#minute').html(new Date().getMinutes());
    $('#date').html(new Date().toDateString());
    $('#zone').html(new Date().toTimeString().slice(9));
    $('#colon').html(':');
}

function validateForm() {
    'use strict'
    const forms = document.querySelectorAll('.requires-validation')
    Array.from(forms)
        .forEach(function (form) {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()
                }
                form.classList.add('was-validated')
            }, false)
        })
}

$(document).ready(function () {
    setInterval(updateTime, 1000);
    setInterval(validateForm, 1000);
    $('#timezone').on('change', function () {
        console.log($('#timezone option:selected').text())
    });
})();

// Show form
// $(document).ready(function () {
//     $(".btn-outline-info").click(function () {
//         $(".form").removeClass('d-none');
//     });
// });
