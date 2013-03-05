// b64
b64_enc = base64.encode
b64_dec = base64.decode
 
// ub64
function ub64_enc(x) {
    return base64.encode(x).replace(/\+/g , '-').replace(/\//g , '_');
}
function ub64_dec(x) {
    return base64.decode(x.replace(/\-/g , '+').replace(/\_/g , '/'));
}

function object_ub64_b64_enc(x) {
    return _.object(_.map(_.pairs(x), function (i) {
        return [ub64_enc(i[0]), b64_enc(i[1])];
    }));
}

function object_ub64_b64_dec(x) {
    return _.object(_.map(_.pairs(x), function (i) {
        return [ub64_dec(i[0]), b64_dec(i[1])];
    }));
}

// json_ub64_b64
function json_ub64_b64_enc(x) {
    return JSON.stringify(object_ub64_b64_enc(x));
}

function json_ub64_b64_dec(x) {
    return object_ub64_b64_dec(JSON.parse(x));
}