$(document).ready(function() {
  var droppedDown = false;
  var fileType = true;
  var token;
  var itemSource;
  var GalaxyNames = ["Galaxian (Erasmus MC)", "CTMM TraIT Demo Galaxy", "Sandbox Galaxy"];
  var GalaxyAddresses = ["http://bioinf-galaxian.erasmusmc.nl/galaxy/tool_runner","http://galaxy-demo.ctmm-trait.nl/tool_runner","http://galaxy-sandbox.trait-ctmm.cloudlet.nl/tool_runner"];

  if (typeof FileActions !== 'undefined') {
    var infoIconPath = OC.imagePath('galaxyconnect', 'external.svg');

    FileActions.register('file', 'Send to Galaxy', OC.PERMISSION_READ, infoIconPath, function(fileName) {
      if (scanFiles.scanning) {
        return;
      }

      var directory = $('#dir').val();
      directory = (directory === "/") ? directory : directory + "/";

      var filePath = directory + fileName;
      var message = t('galaxyconnect', "This will send this file to a Galaxy server of your choice.<br>NOTE: the file will become shared via link in owncloud. <br>You may unshare the file after transfer to Galaxy has completed. <br><br>Select Galaxy server:");
      var ext = fileName.substr(fileName.lastIndexOf('.') + 1);

      //Build dropdown
      var html = "<div id='dropdown' class='drop'>";
      html += "<p id='message'>" + message + "</p>" +
        "<div id='submit'>" +
        "<select id='galaxyServer' name='galaxyServer' >"+
	"<option value='none'> Select Galaxy Server </option> ";
	
      for (var i = 0; i < GalaxyNames.length; i++) {
        if (GalaxyNames[i] != "'" + ext + "'") {
          html += "<option value=" + GalaxyAddresses[i] + ">" + GalaxyNames[i] + "</option>";
        }
      }
      html += "</select>" +	
        "<form method=\"POST\" action=\"\" id=\"myForm\" name=\"myForm\">"+
	  "<input type=\"HIDDEN\" value=\"owncloud_import\" name=\"tool_id\">" +
	  "<input type=\"HIDDEN\" value=\"Human\" name=\"organism\">" +
	  "<input type=\"HIDDEN\" value=\""+fileName+"\" name=\"table\">" +
	  "<input type=\"HIDDEN\" value=\"owncloud file\" name=\"description\">" +
	  "<input type=\"HIDDEN\" value=\"http://bioinf-galaxian.erasmusmc.nl/owncloud/public.php?service=files&t=17adcd7e0ff575a6ae9900cf562c42cf&download\" name=\"URL\" id=\"URL\">" +		
	  "<input type=\"SUBMIT\" value=\"Send this file to Galaxy\" name=\"doGalaxyQuery\">" +
	"</form>"+
        "</div>" +
        "</div>";
     
      if (fileName) {
        $('tr').filterAttr('data-file', fileName).addClass('mouseOver');
	itemSource=$('tr').filterAttr('data-file', fileName).attr('data-id');
        $(html).appendTo($('tr').filterAttr('data-file', fileName).find('td.filename'));

	//dummy call so we dont get undifined
	//OC.Share.share('file',itemSource,3,'',1,'text.txt','',function(result){token= result});
      }

      droppedDown = true;
      console.log("dropped down");
      $('#dropdown').show('blind');
    
     $('#galaxyServer').change(function () {
        OC.Share.share('file',itemSource,3,'',1,'text.txt','',function(result){token= result});
	
        $('#myForm').attr('action', $('#galaxyServer').val());
	
	//once we have our token, set correct URL to send to Galaxy	
	waitForToken();

     }); 
          
    });

  }
  
  $(document).on('dblclick', function(event) {
      hideDropDown();
  }); $('#galaxyServer').val()


  function hideDropDown() {
    $('#dropdown').hide('blind', function() {
      $('#dropdown').remove();
      $('tr').removeClass('mouseOver');
    });
  }

  function waitForToken(){
    //alert("witing for token");
    if(typeof token !== "undefined"){
        //alert(JSON.stringify(token));
        var dlurl = parent.location.protocol+'//'+location.host+OC.linkTo('', 'public.php')+'?service=files&t='+token.token+'&download';
        //alert(dlurl); 
        $('input[name=URL]').val(dlurl);

    }
    else{
        setTimeout(function(){
            waitForToken();
        },250);
    }
  } 
});
