# This Python file uses the following encoding: utf-8
from HTMLParser import HTMLParser
from enum import Enum
import logging

class State(Enum):
  START = 0
  BOARD = 1
  TOP = 2
  FLAVOURS = 3
  FLAVOUR = 4
  BOTTOM = 5

class Shop(Enum):
  NONE = 0
  DANVER = 1
  DELILA = 2
  DAVIS = 3

class FlavourParser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.state = State.START
    self.shop = Shop.NONE
    self.danver_flavours = []
    self.delila_flavours = []
    self.davis_flavours = []
    self.current_flavour = None

  def find_attr(self, attrs, name):
    for attr in attrs:
      if attr[0] == name:
        return attr[1]
    return None

  def handle_starttag(self, tag, attrs):
    if tag == 'img':
      if self.state == State.TOP:
        title = self.find_attr(attrs, 'title')
        if title.find('Danver') >= 0:
          self.shop = Shop.DANVER
        if title.find('Delila') >= 0:
          self.shop = Shop.DELILA
        if title.find('Davis') >= 0:
          self.shop = Shop.DAVIS
    if tag == 'div':
      if self.state == State.START:
        id = self.find_attr(attrs, 'id')
        if id == 'flavourboards':
          self.state = State.BOARD
      elif self.state == State.BOARD:
        clazz = self.find_attr(attrs, 'class')
        if clazz == 'top':
          self.state = State.TOP
        elif clazz == 'flavoursofday':
          self.state = State.FLAVOURS
        elif clazz == 'bottom':
          self.state = State.BOTTOM
      elif self.state == State.FLAVOURS:
        clazz = self.find_attr(attrs, 'class')
        if clazz == 'flavourofday':
          self.state = State.FLAVOUR

  def handle_endtag(self, tag):
    if tag == 'div':
      if self.state == State.BOARD:
        self.state = State.START
      elif self.state == State.TOP:
        self.state = State.BOARD
      elif self.state == State.FLAVOURS:
        self.state = State.BOARD
      elif self.state == State.FLAVOUR:
        if self.shop == Shop.NONE:
          logging.error('Found a flavour without a shop :(')
        elif self.shop == Shop.DANVER:
          self.danver_flavours.append(self.current_flavour)
        elif self.shop == Shop.DAVIS:
          self.davis_flavours.append(self.current_flavour)
        elif self.shop == Shop.DELILA:
          self.delila_flavours.append(self.current_flavour)
        self.current_flavour = None
        self.state = State.FLAVOURS
      elif self.state == State.BOTTOM:
        self.state = State.BOARD

  def handle_data(self, data):
    if self.state == State.FLAVOUR:
      if not self.current_flavour:
        self.current_flavour = data
      else:
        self.current_flavour = self.current_flavour + ' ' + data

html = """
<!doctype html>

<!-- paulirish.com/2008/conditional-stylesheets-vs-css-hacks-answer-neither/ -->
<!--[if lt IE 7 ]> <html lang="en" class="no-js ie6"> <![endif]-->
<!--[if IE 7 ]>    <html lang="en" class="no-js ie7"> <![endif]-->
<!--[if IE 8 ]>    <html lang="en" class="no-js ie8"> <![endif]-->
<!--[if IE 9 ]>    <html lang="en" class="no-js ie9"> <![endif]-->
<!--[if (gt IE 9)|!(IE)]><!--> <html lang="en" class="no-js"> <!--<![endif]-->
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />

	<title>GandD's Cafe | Today's Flavours | GandD's Ice Cream Cafes - Oxford's Own Ice Cream </title>



	<link href="http://www.gdcafe.com/website/css/reset.css" rel="stylesheet" type="text/css" />
<link href="http://www.gdcafe.com/website/css/GD.css" rel="stylesheet" type="text/css" />
<link rel="stylesheet" href="http://www.gdcafe.com/website/css/nivo-slider.css" type="text/css" media="screen" />
    <link rel="stylesheet" href="http://www.gdcafe.com/website/css/style.css" type="text/css" media="screen" />
 <script type="text/javascript">
<!--
function MM_swapImgRestore() { //v3.0
  var i,x,a=document.MM_sr; for(i=0;a&&i<a.length&&(x=a[i])&&x.oSrc;i++) x.src=x.oSrc;
}
function MM_preloadImages() { //v3.0
  var d=document; if(d.images){ if(!d.MM_p) d.MM_p=new Array();
    var i,j=d.MM_p.length,a=MM_preloadImages.arguments; for(i=0; i<a.length; i++)
    if (a[i].indexOf("#")!=0){ d.MM_p[j]=new Image; d.MM_p[j++].src=a[i];}}
}

function MM_findObj(n, d) { //v4.01
  var p,i,x;  if(!d) d=document; if((p=n.indexOf("?"))>0&&parent.frames.length) {
    d=parent.frames[n.substring(p+1)].document; n=n.substring(0,p);}
  if(!(x=d[n])&&d.all) x=d.all[n]; for (i=0;!x&&i<d.forms.length;i++) x=d.forms[i][n];
  for(i=0;!x&&d.layers&&i<d.layers.length;i++) x=MM_findObj(n,d.layers[i].document);
  if(!x && d.getElementById) x=d.getElementById(n); return x;
}

function MM_swapImage() { //v3.0
  var i,j=0,x,a=MM_swapImage.arguments; document.MM_sr=new Array; for(i=0;i<(a.length-2);i+=3)
   if ((x=MM_findObj(a[i]))!=null){document.MM_sr[j++]=x; if(!x.oSrc) x.oSrc=x.src; x.src=a[i+2];}
}
//-->
</script>

<meta name="description" content="Our flavours of Ice Cream change on a daily basis. Check back often to find out which flavours are being served at which shop today! G&Ds is Oxford's premier independent ice cream cafe. G&Ds specialises in natural, home-made ice cream and baked goods. We serve fresh bagels, salads and offer the finest, ethically sourced coffees around. ">
<meta name="keywords" content="Today's Flavours, Ice Cream, George, Danver, Delilah, Davis, G&Ds, Cafe, Oxford, England, Bagel Sandwich, Waffle Sundae, Coffee Shop, Ice Cream Cake">
<meta name="author" content="Alissa J. Robinson - http://www.alissajrobinson.co.uk">
</head>

<body class="oneColFixCtrHdr">
<div id="gradient">
<div id="container">
  <div id="header">
  <a href="http://www.gdcafe.com/website/index.php"><img src="http://www.gdcafe.com/website/images/spacer.gif" alt="GandD's Ice Cream Cafe" class="home" title="GandD's Ice Cream Cafe" width="170" height="130" /></a>
  <a href="http://www.gdcafe.com/website/index.php"><img src="http://www.gdcafe.com/website/images/logo-text.png" alt="Oxfords Own Ice Cream"  class="logo" title="Oxfords Own Ice Cream" /></a>


<div id="sign2"><a  class="sign2" href="http://www.gdcafe.com/website/index.php/Flavours">Todays Flavours</a><span></span></div>




  <ul id="menu">
<li><a class="about" href="http://www.gdcafe.com/website/index.php/About">About Us<span></span></a></li>
<li><a class="locations" href="http://www.gdcafe.com/website/index.php/Locations">Locations<span></span></a></li>
<li><a class="products" href="http://www.gdcafe.com/website/index.php/Products">Products<span></span></a></li>
<li><a class="events" href="http://www.gdcafe.com/website/index.php/Events">Events<span></span></a></li>
<!--<li><a class="reviews" href="http://www.gdcafe.com/website/index.php/Reviews">Reviews<span></span></a></li>-->
<li><a class="jobs" href="http://www.gdcafe.com/website/index.php/Jobs">Jobs<span></span></a></li>
</ul>
  <!-- end #navigation -->
<!-- end #header --></div>

  <div id="mainContent">
   <a href="http://www.gdcafe.com/website/index.php/Locations"><img src="http://www.gdcafe.com/website/images/finger.png" alt="GandD's Cafe" width="153" height="95" class="finger" /> </a>
<div id="cone2"><a  class="cone2" href="http://www.gdcafe.com/website/index.php/Locations"> cone</a><span></span></div>


   <div id="insidecontent">
<h1>Today's Flavours</h1>


<div id="flavourboards">
<div class="top"><img src="http://www.gdcafe.com/website/images/flavours/davis1.gif" title="George and Davis Flavour Board" alt="George and Davis Flavour Board" /></div>
<div class="flavoursofday">

<div class="flavourofday">Greek Yogurt & Ginger</div>

<div class="flavourofday">Black Beauty (Blackberry & Honey)</div>

<div class="flavourofday">Oreo's</div>

<div class="flavourofday">Coffee</div>

<div class="flavourofday">Dimebar Crunch</div>

<div class="flavourofday">Mango Sorbet</div>

<div class="flavourofday">Raspberry Sorbet</div>

<div class="flavourofday">Rum & Raisin</div>

<div class="flavourofday">St Clements</div>

<div class="flavourofday">Strawberry</div>

<div class="flavourofday">Super #?*! Chocolate</div>

<div class="flavourofday">Vanilla</div>

</div>
<div class="bottom">&nbsp;</div>
<p class="smalltext">* last updated: 23 03 2015, 12:26</p>
</div>




<div id="flavourboards">
<div class="top"><img src="http://www.gdcafe.com/website/images/flavours/danver2.gif" title="George and Danver Flavour Board" alt="George and Danver Flavour Board" /></div>
<div class="flavoursofday">

<div class="flavourofday">Baileys & Sweetcream</div>

<div class="flavourofday">Black Beauty (Blackberry & Honey)</div>

<div class="flavourofday">Coffee</div>

<div class="flavourofday">Dimebar Crunch</div>

<div class="flavourofday">Greek Yoghurt & Ginger</div>

<div class="flavourofday">Mango Sorbet</div>

<div class="flavourofday">Mars Mania</div>

<div class="flavourofday">Raspberry Sorbet</div>

<div class="flavourofday">Rum & Raisin</div>

<div class="flavourofday">Strawberry</div>

<div class="flavourofday">Super #?*! Chocolate</div>

<div class="flavourofday">Vanilla</div>

</div>
<div class="bottom">&nbsp;</div>
<p class="smalltext">* last updated: 23 03 2015, 12:28</p>
</div>




<div id="flavourboards">
<div class="top"><img src="http://www.gdcafe.com/website/images/flavours/delila3.gif" title="George and Delila Flavour Board" alt="George and Delila Flavour Board" /></div>
<div class="flavoursofday">

<div class="flavourofday">After Midnight</div>

<div class="flavourofday">Baileys & Sweetcream</div>

<div class="flavourofday">Black Beauty (Blackberry & Honey)</div>

<div class="flavourofday">Coffee</div>

<div class="flavourofday">Dimebar Crunch</div>

<div class="flavourofday">Greek Yogurt & Ginger</div>

<div class="flavourofday">Mango Sorbet</div>

<div class="flavourofday">Mars Mania</div>

<div class="flavourofday">St Clements</div>

<div class="flavourofday">Strawberry</div>

<div class="flavourofday">Super #?*! Chocolate</div>

<div class="flavourofday">Vanilla</div>

</div>
<div class="bottom">&nbsp;</div>
<p class="smalltext">* last updated: 23 03 2015, 12:25</p>
</div>

<br class="clearboth" />

<!--

<p>The idea for G&amp;D’s developed out of the experience of an Oxford University student, George Stroup, who founded the business in order to provide a few basic things for the local community: great ice cream, reasonably priced quality food, friendly, convenient service and a bright, unpretentious atmosphere.</p>

<p>Before G&amp;D’s, Oxford lacked good ice cream. Consumers were stuck with a &#8216;non-choice&#8217; of low quality national brands and the &#8216;cheap and cheerful&#8217; stuff sold from roving vans - typically these products contained a myriad of artificial ingredients, colours, stabilizers and softeners, and often lacked any cream at all! (Sadly, the latter was permitted by labelling laws.) </p>

<p>Another key motivation for starting G&amp;D&#8217;s was that Oxford lacked bright, easy-going places where you could stop-in and have a hot drink and something to eat without suffering the triple insult of indifferent service, inflated prices and dire food. </p>

<p>Against this background, George was convinced that Oxford was ripe for the fusion of ideas he called the &#8216;Ice Cream Café&#8217; which had been evolving in his mind almost from the day he first arrived. Finally, in the Spring of 1991 after overhearing yet another group of people - this time at Oriel College - discussing the Oxford scene such that they essentially listed the key motivations for the Ice Cream Cafe, George decided it was time to move from concept (and what had become a fairly detailed business plan) to reality. Over the next several months he - with the assistance of a host of friends and other helpers - found suppliers of fresh rich cream and other natural ingredients to make a range of creative &#8216;super premium&#8217; ice cream flavours; travelled to an ice cream machine company in the USA and asked them to design a top-of-the-line machine that would always make great ice cream (the head engineer kept his promise to make a machine &#8216;in the spirit of Rolls Royce&#8217;); located a convenient and central shop space in Little Clarendon Street; assembled all the necessary kitchen equipment, work tops, tables, chairs, display freezers, crockery, etc. Long hours of loading and unloading, sawing, hammering and painting followed. When the dust settled it was the summer of 1992 and G&amp;D’s was born!</p>


   -->

</div>
  <!-- end #mainContent --></div>
 <div id="footer"><!--<div id="cowblog"><a href="http://www.gdcafe.com/website/index.php/Blog" title="Read Marcus' Blog"><img src="http://www.gdcafe.com/website/images/spacer.gif" alt="Read Marcus Blog" width="158" height="133" /></a></div>-->
<div id="facebook"><a href="http://www.facebook.com/pages/GDs-Ice-Cream-Caf%C3%A9s/182860828323" title="Follow us on Facebook" target="_blank"><img src="http://www.gdcafe.com/website/images/spacer.gif" alt="Follow us on Facebook" title="Follow us on Facebook" width="48" height="58" /></a></div>
<div id="twitter"><a href="http://twitter.com/gdcafe" title="Follow us on Twitter" target="_blank"><img src="http://www.gdcafe.com/website/images/spacer.gif" alt="Follow us on Twitter" title="Follow us on Twitter" width="48" height="58" /></a></div>
    <div class="copyright"><p> <strong>G&amp;Ds specialises in natural, home-made ice cream and baked goods. We serve fresh bagels, salads and offer the finest, ethically sourced coffees around. <br /> Open from 8am till midnight everyday.<br /><a href="mailto:feedback@gdcafe.com">Contact Us</a></strong><br />&copy;Copyright G&amp;D's. All rights reserved. Website design by <a href="http://www.alissajrobinson.co.uk" target="_blank">Alissa J. Robinson</a>
<br />All photos by <a href="http://www.darkbluephotography.com/" target="_blank">Dark Blue Photography</a></p></div>
</div>

<!-- end #gradient --></div>
<!-- end #container --></div>

</body>
</html>
"""

if __name__ == "__main__":
  parser = FlavourParser()
  parser.feed(html)

  print parser.delila_flavours
  print parser.davis_flavours
  print parser.danver_flavours