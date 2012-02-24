var p = "<div style=\"clear:both\"></div>guest@zmbush.com $ "
var text = '<br /><br /><br />Type `help` for a list of commands.<br />'
processCommand('pwd', initPrompt, true);
var command = ""
var cursor = "_"
var accepting_input = true;
var previous_commands = new Array();
var command_index = 0
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
      switch(e.which){
        case 8:
          if(command.length > 0){
            command = command.substring(0, command.length - 1)
            $('#term').html(text + command + cursor);
          }
          return false;
          break;
        case 38: // up
          if(command_index > 0){
            command_index--;
            command = previous_commands[command_index]
            $('#term').html(text + command + cursor);
          }
          return false;
        case 40: // Down
          if(command_index < previous_commands.length - 1){
            command_index++;
            command = previous_commands[command_index]
            $('#term').html(text + command + cursor);
          }else{
            command_index = previous_commands.length;
            command = '';
            $('#term').html(text + command + cursor);
          }
          return false;
      }
    }
  });
  $('#term').html(text);
});

function processCommand(cin, callback, quiet){
  if(!quiet){
    if(previous_commands[previous_commands.length - 1] != cin && cin != ''){
      previous_commands.push(cin)
    }
    command_index = previous_commands.length;
  }
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
      window.location = 'http://www.zmbush.com/static/';
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
        arg = arg.replace(/\//g, '|-|').replace(/\./g, '|_|')
      }
      $.ajax({
        url: '/' + command + '/' + arg,
        dataType: "json",
        error: function(){
          callback(cin + ": connection to remote server lost.");
        },
        success: function(output){
          if (output.command == 'cd') {
            setPrompt(output.output)
            callback('')
          }else
            callback(output.output);
        }
      });
  }
}

function displayOutput(output){
  if(output != '')
    text += output + "<br />";
  newPrompt()
}

function newPrompt(){
  text += p;
  accepting_input = true;
  command = '';
  $('#term').html(text);
  $("html, body").animate({ scrollTop: $(document).height() }, "fast");
}

function initPrompt(text){
  setPrompt(text)
  newPrompt()
}
function setPrompt(text){
  p = "guest@zmbush.com " + text + " $ "
}
