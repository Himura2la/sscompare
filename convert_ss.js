const Ss = require('./simple-second/lib/ss.js')

const input_timestamp = parseInt(process.argv[2])
const ss_timestamp = Math.round((1000/864)*(new Date(input_timestamp)-2*60*60*1000)+((1492*365+477*366)*100000000))
const ss = new Ss(ss_timestamp)
const response = {
    'year': ss.getYear(),
    'month': ss.getMonth(),
    'day': ss.getDay(),
    'time': ss.getTime(),
    'week': ss.getWeek(),
    'week_day': ss.getDayOfWeek()
}
console.log(JSON.stringify(response))
