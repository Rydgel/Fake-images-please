clic = (dom_id, width=500, height=300) ->
	dom_id.onclick = () ->
		window.open dom_id.href, "", "width=#{width}, height=#{height}"
		false

id = (dom_id) ->
	document.getElementById(dom_id)
		
window.onload = () ->
	tweet_id = id "tweet"
	facebook_id = id "facebook"
	
	clic tweet_id if tweet_id
	clic facebook_id, 640, 280 if facebook_id
