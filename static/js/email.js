(function(){
      emailjs.init("user_rNlxjH93KI0o2WUxLY4rd");
   })();

function sendMail(contactForm) {
    emailjs.send("gmail", "recycling_hive", {
        "from_name": contactForm.name.value,
        "from_email": contactForm.email.value,
        "subject": contactForm.subject.value,
        "message": contactForm.message.value
    })
    .then(
        function(response) {
            $("#contact-flash").show();
            $("#contact-form")[0].reset();
        }
    );
    return false;
}