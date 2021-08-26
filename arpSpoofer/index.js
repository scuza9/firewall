const ip = require('ip');
const arp = require('arpjs')
const fs = require('fs')
const local = require('ipmask')()
const address = require('address')
const Arpping = require('arpping');
const arpping = new Arpping();

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

