var p = "<div style=\"clear:both\"></div>guest@zmbush.com $ "
var text = '<br /><br /><br />Type `help` for a list of commands.<br />'
processCommand('whoami', initPrompt, true);
var user = 'guest'
var command = ""
var directory = '/'
var input = ""
var cursor = "_"
var accepting_input = true;
var previous_commands = new Array();
var echo_input = true;
var function_input = false;
var command_index = 0
var previous_results = null;


function cleanArray(actual, deleteValue){
  var newArray = new Array();
  for(var i = 0; i<actual.length; i++){
    if (actual[i] != deleteValue){
      newArray.push(actual[i]);
    }
  }
  return newArray;
}
function displayCommand(){
  newhtml = text
  if(function_input){
    if(echo_input){
      newhtml += input
    }else{
      newhtml += input.replace(/./g, '*')
    }
  }else{
    if(echo_input){
      newhtml += command
    }else{
      newhtml += command.replace(/./g, '*')
    }
  }
  $('#term').html(newhtml + cursor)
}

$(function(){
  $(document).keypress(function(e){
    if(accepting_input){
      switch(e.which){
        case 8:
          return false;
        case 13:
          if(function_input){
            if(echo_input){
              text += input
            }else{
              text += input.replace(/./g, '*')
            }
          }else{
            if(echo_input){
              text += command;
            }else{
              text += command.replace(/./g, '*')
            }
          }
          text += '<br />';
          accepting_input = false;
          $('#term').html(text + '...');
          if(function_input){
            command = previous_results.command;
            command += " " + previous_results.args.join(" ")
            command += " " + input
            processCommand(command, displayOutput);
          }else{
            processCommand(command, displayOutput);
          }
          return false;
        default:
          if(function_input){
            input += String.fromCharCode(e.which);
          }else{
            command += String.fromCharCode(e.which);
          }
          displayCommand();
          return false;
      }
    }
  });
  $(document).keydown(function(e){
    if(accepting_input){
      switch(e.which){
        case 8:
          if(function_input){
            if(input.length > 0){
              input = input.substring(0, input.length - 1)
              displayCommand();
            }
          }else{
            if(command.length > 0){
              command = command.substring(0, command.length - 1)
              displayCommand();
            }
          }
          return false;
          break;
        case 38: // up
          if(!function_input){
            if(command_index > 0){
              command_index--;
              command = previous_commands[command_index]
              $('#term').html(text + command + cursor);
            }
          }
          return false;
        case 40: // Down
          if(!function_input){
            if(command_index < previous_commands.length - 1){
              command_index++;
              command = previous_commands[command_index]
              $('#term').html(text + command + cursor);
            }else{
              command_index = previous_commands.length;
              command = '';
              $('#term').html(text + command + cursor);
            }
          }
          return false;
      }
    }
  });
  $('#term').html(text);
});

function processCommand(cin, callback, quiet){
  if(!quiet && echo_input){
    if(previous_commands[previous_commands.length - 1] != cin && cin != ''){
      previous_commands.push(cin)
    }
    command_index = previous_commands.length;
  }
  switch(cin){
    case '':
      newPrompt();
      break;
    // case 'linkedin':
      // window.location = "http://www.linkedin.com/pub/zachary-bush/1a/a78/671";
      // break;
    // case 'github':
      // window.location = "https://github.com/zipcodeman";
      // break;
    // case 'static':
      // window.location = 'http://www.zmbush.com/static/';
      // break;
    // case 'exit':
      // window.location = 'http://www.google.com/';
      // break;
    default:
      args = cin.split(' ')
      command = args[0];
      if(args.length > 0){
        args.shift()
        args = cleanArray(args, "")
        arg = args.join(';')
        arg = arg.replace(/\//g, '|-|').replace(/\./g, '|_|')
      }
      $.ajax({
        url: './' + command + '/' + arg,
        dataType: "json",
        error: function(){
          callback(cin + ": there was a problem executing your command.");
        },
        success: function(output){
          echo_input = true
          function_input = false
          previous_results = output
          if (output.command == 'cd') {
            directory = output.output
            setPrompt()
            callback('')
          }else if(output.output.indexOf('REDIRECT: ') == 0){
            window.location = output.output.split(' ')[1]
            displayOutput('Redirecting...')
          }else if(output.output.indexOf('GET: ') == 0){ 
            // Get a string and send it back to the function.
            function_input = true
            displayOutput('')
          }else if(output.output.indexOf('GETQ: ') == 0){
            // Get a string quietly and send it back to the function.
            function_input = true
            echo_input = false
            displayOutput("")
          }else if(output.command == 'login' || output.command == 'logout'){
            processCommand('whoami', initPrompt, true);
          }else{
            callback(output.output);
          }
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
  if(function_input){
    text += '> '
  }else{
    text += p;
  }
  accepting_input = true;
  if(function_input){
    input = '';
  }else{
    command = '';
  }
  $('#term').html(text);
  $("html, body").animate({ scrollTop: $(document).height() }, "fast");
}

function initPrompt(text){
  user = text;
  processCommand('pwd', promptDir, true);
}

function promptDir(text){
  directory = text
  setPrompt()
  newPrompt()
}
function setPrompt(){
  p = '<div style="clear:both"></div>' + user + "@zmbush.com " + directory + " $ "
}
