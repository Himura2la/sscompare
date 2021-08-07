const ssLib = require('./simple-second/lib/ss.js')

const input_timestamp = parseInt(process.argv[2])
const ss = ssLib.dateToSs(new Date(input_timestamp))
const response = {
    'year': ss.getYear(),
    'month': ss.getMonth(),
    'day': ss.getDay(),
    'time': ss.getTime(),
    'week': ss.getWeek(),
    'week_day': ss.getDayOfWeek()
}
console.log(JSON.stringify(response))
