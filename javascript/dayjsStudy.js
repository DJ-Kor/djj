// import dayjs from 'dayjs';
const dayjs = require("dayjs");

const curYear = dayjs().year();

const curYearFirstDay = dayjs(`${curYear}-01-01`, "YYYY-MM-DD");
const curYearLastDay = dayjs(`${curYear}-12-31`);

console.log(curYear);
console.log(curYearFirstDay.valueOf(), curYearFirstDay.format());
console.log(curYearLastDay.valueOf(), curYearLastDay.format());

console.log(typeof curYearFirstDay);

const ut = dayjs(1720596201000);
console.log(ut.format());
const utu = dayjs.unix(1720596201000);
console.log(utu.format());

console.log("standby_project_status.js:92 row.createdAt", dayjs(1722302246000).format(), "1724-06-23T22:00:00+08:30");
console.log("standby_project_status.js:92 row.createdAt", dayjs(1723779448000).format(), "1729-08-04T00:00:00+08:30");
console.log("standby_project_status.js:92 row.createdAt", dayjs(1716794878000).format(), "1722-08-20T06:00:00+08:30");
console.log("standby_project_status.js:92 row.createdAt", dayjs(1723779448000).format(), "1729-08-04T00:00:00+08:30");
console.log("standby_project_status.js:92 row.createdAt", dayjs(1723598063000).format(), "1728-01-21T15:00:00+08:30");
console.log("standby_project_status.js:92 row.createdAt", dayjs(1723779448000).format(), "1729-08-04T00:00:00+08:30");
console.log("standby_project_status.js:92 row.createdAt", dayjs(1716791760000).format(), "1722-07-19T12:00:00+08:30");
console.log("standby_project_status.js:92 row.createdAt", dayjs(1716794878000).format(), "1722-08-20T06:00:00+08:30");
console.log("standby_project_status.js:92 row.createdAt", dayjs(1723598063000).format(), "1728-01-21T15:00:00+08:30");
console.log("standby_project_status.js:92 row.createdAt", dayjs(1723779448000).format(), "1729-08-04T00:00:00+08:30");
console.log("standby_project_status.js:92 row.createdAt", dayjs(1716794878000).format(), "1722-08-20T06:00:00+08:30");
console.log("standby_project_status.js:92 row.createdAt", dayjs(1720596201000).format(), "1725-01-01T01:00:00+08:30");
console.log("standby_project_status.js:92 row.createdAt", dayjs(1722302246000).format(), "1724-06-23T22:00:00+08:30");

const dateToString = (date) => {
  let offset = date.getTimezoneOffset() * 60000;
  let dateOffset = new Date(date.getTime() - offset);
  return dateOffset.toISOString().split("T")[0];
};

const today = new Date();
const thisYear = today.getFullYear();

const startDate = new Date(thisYear, today.getMonth(), 1);
const endDate = new Date(thisYear, today.getMonth(), today.getDate());

console.log("startDate, ", startDate);
console.log("endDate, ", endDate);

console.log("startDate, ", dateToString(startDate));
console.log("endDate, ", dateToString(endDate));

console.log(typeof dateToString(startDate));
