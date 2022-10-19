import BlynkLib from 'blynk-library';

const blynk = new BlynkLib.Blynk('715f8caae9bf4a91bae319d0376caa8d');
const v1 = new blynk.VirtualPin(1);
const v9 = new blynk.VirtualPin(9);

v1.on('write', function(param) {
  console.log('V1:', param);
});

v9.on('read', function() {
  v9.write(new Date().getSeconds());
});
