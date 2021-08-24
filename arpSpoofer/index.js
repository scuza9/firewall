const ip = require('ip');
const arp = require('arpjs')
const fs = require('fs')
const local = require('ipmask')()
const address = require('address')

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

arp.table(function (err, table) {
    fs.writeFile('arpLocal.log', JSON.stringify(table, null, 2), err => {
        if (err) {
          console.error(err)
          return
        }
      })
})
});


