var p = "<div style=\"clear:both\"></div>guest@zmbush.com $ "
var text = '<br /><br /><br />Type `help` for a list of commands.<br />'
processCommand('pwd', setPrompt);
var command = ""
var cursor = "_"
var accepting_input = true;
$(function(){
  $(document).keypress(function(e){
    if(accepting_input){
      switch(e.which){
        case 8:
          return false;
        case 13:
          text += command;
          text += '<br />';
          accepting_input = false;
          $('#term').html(text + '...');
          processCommand(command, displayOutput);
          return false;
        default:
          command += String.fromCharCode(e.which);
          $('#term').html(text + command + cursor);
          return false;
      }
    }
  });
  $(document).keydown(function(e){
    if(accepting_input){
      if(e.which == 8){
        if(command.length > 0){
          command = command.substring(0, command.length - 1)
          $('#term').html(text + command + cursor);
        }
        return false;
      }
    }
  });
  $('#term').html(text);
});

function processCommand(cin, callback){
  switch(cin){
    case '':
      newPrompt();
      break;
    case 'linkedin':
      window.location = "http://www.linkedin.com/pub/zachary-bush/1a/a78/671";
      break;
    case 'github':
      window.location = "https://github.com/zipcodeman";
      break;
    case 'static':
      window.location = '/static/';
      break;
    case 'exit':
      window.location = 'http://www.google.com/';
      break;
    default:
      args = cin.split(' ');
      command = args[0];
      if(args.length > 0){
        args.shift()
        arg = args.join(';')
      }
      $.ajax({
        url: '/' + command + '/' + arg,
        dataType: "html",
        error: function(){
          callback(cin + ": Bad things happened...");
        },
        success: function(output){
          callback(output);
        }
      });
  }
}

function displayOutput(output){
  text += output;
  newPrompt()
}

function newPrompt(){
  text += p;
  accepting_input = true;
  command = '';
  $('#term').html(text);
  $("html, body").animate({ scrollTop: $(document).height() }, "slow");
}

function setPrompt(text){
  dirs = text.split("/")
  fold = dirs[dirs.length - 2]
  p = "guest@zmbush.com " + fold + " $ "
  newPrompt();
}
