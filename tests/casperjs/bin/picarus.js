var casper = require('casper').create({
    verbose: true,
    logLevel: "debug"
});

EMAIL = casper.cli.get('email')
API_KEY = casper.cli.get('api_key')
LOGIN_KEY = casper.cli.get('login_key')
OTP = casper.cli.get('otp')
SERVER = casper.cli.get('server')

casper.start(SERVER, function() {
    /*
    this.echo(this.evaluate(function (otp, email, loginKey) {
        $('#email').val(email);
        $('#loginKey').val(loginKey);
        $('#otp').val(otp);
        $('#otp').trigger('keypress');
    }, OTP, EMAIL, LOGIN_KEY));
    */
    this.evaluate(function (apiKey, email, loginKey) {
        $('#email').val(email);
        $('#loginKey').val(loginKey);
        $('#apiKey').val(apiKey);
        $('#apiKey').trigger('keypress');
    }, API_KEY, EMAIL, LOGIN_KEY);
    this.waitWhileVisible('#authModal', function () {
        email_auth = this.getGlobal('EMAIL_AUTH')
        this.echo(JSON.stringify(email_auth));
        this.test.assertEquals(email_auth.email, EMAIL);
        this.test.assertEquals(email_auth.auth, API_KEY);
    });
    this.waitUntilVisible('#results', function () {
        this.test.pass('Results visible');
    });
    
    // Run a thumbnail job
    this.evaluate(function () {
        window.location.hash = '#process/thumbnail';
    });

    this.waitForSelector('#runButton', function () {
        this.evaluate(function () {
            $('#runButton').click();
        }, function () {}, 15000);
    });
    this.waitForSelector('#runButton:disabled', function () {
        this.test.pass('Job Started');
    }, function () {}, 15000);
    this.waitWhileSelector('#runButton:disabled', function () {
        this.test.pass('Job done');
    }, function () {}, 120000);
});
casper.run();