var casper = require('casper').create({
    verbose: true,
    logLevel: "debug"
});

OTP = ''
EMAIL = ''
LOGIN_KEY = ''

casper.start('https://api.picar.us', function() {
    this.echo(this.evaluate(function (otp, email, loginKey) {
        $('#email').val(email);
        $('#loginKey').val(loginKey);
        $('#otp').val(otp);
        $('#otp').trigger('keypress');
    }, OTP, EMAIL, LOGIN_KEY));
    this.waitWhileVisible('#authModal', function () {
        this.echo(JSON.stringify(this.getGlobal('EMAIL_AUTH')));
    });
    this.waitUntilVisible('#results', function () {
        this.echo('Results visible');
    });
    
    // Run a thumbnail job
    this.evaluate(function () {
        window.location.hash = '#process/thumbnail';
    });

    this.waitForSelector('#runButton', function () {
        this.evaluate(function () {
            $('#runButton').click();
        });
    });
    this.waitForSelector('#runButton:disabled', function () {
        this.echo('Job Started');
    });
    this.waitWhileSelector('#runButton:disabled', function () {
        this.echo('Job done');
    }, function () {}, 120000);
});
casper.run();