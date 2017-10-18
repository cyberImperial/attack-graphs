const jquery = require("jquery");
const host = "http://127.0.0.1:4242";

jquery.ajax({
  type: "GET",
  url: host,
  success: function (data) {
    console.log(data);
  }
});
