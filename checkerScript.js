function print(message){
	console.log(message);
}

function sendEmail(subject, message){
	
	/* SmtpJS.com - v3.0.0 */
	var Email = { send: function (a) { return new Promise(function (n, e) { a.nocache = Math.floor(1e6 * Math.random() + 1), a.Action = "Send"; var t = JSON.stringify(a); Email.ajaxPost("https://smtpjs.com/v3/smtpjs.aspx?", t, function (e) { n(e) }) }) }, ajaxPost: function (e, n, t) { var a = Email.createCORSRequest("POST", e); a.setRequestHeader("Content-type", "application/x-www-form-urlencoded"), a.onload = function () { var e = a.responseText; null != t && t(e) }, a.send(n) }, ajax: function (e, n) { var t = Email.createCORSRequest("GET", e); t.onload = function () { var e = t.responseText; null != n && n(e) }, t.send() }, createCORSRequest: function (e, n) { var t = new XMLHttpRequest; return "withCredentials" in t ? t.open(e, n, !0) : "undefined" != typeof XDomainRequest ? (t = new XDomainRequest).open(e, n) : t = null, t } };
	
	Email.send({Host : "smtp.elasticemail.com",
				Username : YourUserName,
				Password : YourPassword,
				To : emailAddress,
				From : emailAddress,
				Subject : subject,
				Body : message
				}).then(message => alert(message));
}

function myFunction(data, expectedDate) {
	data.sort(function (a, b) {
		return new Date(a.date).getTime() - new Date(b.date).getTime();
	});
	
	var message = [];
	for(i = 0; i < data.length; i++)
	{
	  message.push(data[i].date);
	}
	message.join("\n");
	
	print('return array length is ' + data.length);

	if(data.length > 0)
	{
		print('Available Dates are: \n' + message);
		
		var earliestDate = data[0].date;
		
		if(new Date(earliestDate) < new Date(expectedDate))
		{
			print('There are available dates before ' + expectedDate);
			sendEmail("VISA New Opening: " + earliestDate, message);
			print('Email notification sent!');
		}
	}
}

function Check()
{
	print('=======================');
	print('Start to check');

	var xmlhttp = new XMLHttpRequest();
	var url = "https://ais.usvisa-info.com/en-ca/niv/schedule/23907112/appointment/days/95.json?appointments[expedite]=false";

	xmlhttp.onreadystatechange = function() {
		if(this.readyState == 4){
			var data = JSON.parse(this.responseText);
			if(data.error != null){
				return false;
			}
			
			var expectedDate = '2019-03-15';
			myFunction(data, expectedDate);
		}
	};
	xmlhttp.open("GET", url, true);
	xmlhttp.send();
	print('Success checked');
	return true;
}

let timerId = setTimeout(function tick() {
  var alive = Check();
  if(alive == true){
	print('Schedule next check');
	timerId = setTimeout(tick, 300000); // (*)
  }
  else{
	  sendEmail("session end.", "session end.");
  }
}, 1000);
