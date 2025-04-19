<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Top 5 Similar Songs</title>
  <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
  <!--<link rel="icon" href="./public/icon.png" /> -->
 </head>
 <body class = "bg-white">
  <nav class="bg-sky-300 rounded-sm border-gray-200 flex items-center justify-between">
          <!--<img src="./public/icon.png" style="width: 50px; height: 50px;" class="ml-2 mb-4" alt="Gun Range Search Site Logo" />-->
          <div class="hidden w-full md:block md:w-auto" id="navbar-default">
              <ul class="font-medium flex flex-row p-4 md:p-0 ml-4 mr-16 mt-12">
              <li>
                  <a href="http://localhost/similar-music-finder/index.html" class="block py-2 px-3 text-white hover:underline" aria-current="page">Home</a>
              </li>
              </ul>
          </div>
          </div>
    </nav>
    <h1 class="text-6xl font-bold italic font-mono text-center text-yellow-950 pt-4">
        Search Results
    </h1>
  <?php
    
    // PHP code just started

    // display errors
    ini_set('error_reporting', E_ALL);
    ini_set('display_errors', true);
    

    //enable exceptions
    mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);

    try {
    
      // Undefined | Multiple Files | $_FILES Corruption Attack
      // If this request falls under any of them, treat it invalid.
      if (
          !isset($_FILES['query']['error']) ||
          is_array($_FILES['query']['error'])
      ) {
          throw new RuntimeException('Invalid parameters.');
      }
  
      // Check $_FILES['upfile']['error'] value.
      switch ($_FILES['query']['error']) {
          case UPLOAD_ERR_OK:
              break;
          case UPLOAD_ERR_NO_FILE:
              throw new RuntimeException('No file sent.');
          case UPLOAD_ERR_INI_SIZE:
          case UPLOAD_ERR_FORM_SIZE:
              throw new RuntimeException('Exceeded filesize limit.');
          default:
              throw new RuntimeException('Unknown errors.');
      }
  
      // You should also check filesize here. 
      if ($_FILES['query']['size'] > 1000000) {
          throw new RuntimeException('Exceeded filesize limit.');
      }
      
      //looks like the file download is having issues...
      $uploads_dir = 'user-input';
      $download_loc = '';
      foreach ($_FILES["query"]["error"] as $key => $error) {
          if ($error == UPLOAD_ERR_OK) {
              $tmp_name = $_FILES["query"]["tmp_name"][$key];
              // basename() may prevent filesystem traversal attacks;
              $name = basename($_FILES["query"]["name"][$key]);
              $download_loc = "$uploads_dir/$name";
              move_uploaded_file($tmp_name, $download_loc);
          }
      }

      $results = shell_exec("python process_music.py " .$download_loc); //should return an array?
      $col_names = array("Song");
      //display the results in a table
      echo "<table class='ml-2 mt-2 border-2 border-black shadow-lg' style='border: border-collapse: collapse; margin-left: auto; margin-right: auto; width: 50%;'>\n"; 
      echo "<tr>";
      foreach($col_names as $name) {
        echo "<th style='border: 1px solid black; padding: 8px;'>" . $name . "</th>";
      }
      echo "</tr>\n";

      foreach($results as $result) {
        echo "<tr>";
          //maybe in the future loop through more than just song name...
          echo "<td style='border: 1px solid black; padding: 8px;'>" . $result . "</td>";
            
        echo "</tr>\n";
      }
          
      echo "</table>\n";

  
      //remove the file when done to save space
      if (!unlink($download_loc)) { 
        echo ("$download_loc cannot be deleted due to an error"); 
      } else { 
        echo ("$file_pointer has been deleted"); 
      }
  
  } catch (RuntimeException $e) {
  
      echo $e->getMessage();
  
  }
      
  ?>
  <div class = "flex relative">
    <div id = "re-query_area" class = "mt-8 ml-8 p-2">
          <p class = "text-xl font-bold italic mb-2">Searh for with a new song:</p> <!--do I even want this?-->
          <form action="index.php" method="post" accept-charset="utf-8" class="inline-flex items-end space-x-4">
              <textarea class = "outline rounded shadow-lg" name="sql_query" rows="9" cols="50"></textarea>
          <input type="Submit" class = "outline rounded bg-white p-2">
          </form>
    </div>
  </div>

</body>
