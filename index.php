<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Top 5 Similar Songs</title>
  <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
  <link rel="icon" href="./public/icon.png" />
 </head>
 <body class = "bg-white">
  <nav class="bg-cyan-200 rounded-sm border-gray-200 flex items-center justify-between">
        <img src="./public/icon.png" style="width: 100px; height: 100px;" class="ml-2 mb-4 mt-4" alt="Music Finder Logo" />
          <div class="hidden w-full md:block md:w-auto" id="navbar-default">
              <ul class="font-medium flex flex-row p-4 md:p-0 ml-4 mr-16 mt-12">
              <li>
                  <a href="http://localhost/music-IR/index.html" class="block py-2 px-3 mt-10 text-black hover:underline text-2xl" aria-current="page">Home</a>
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
      
      
      $uploads_dir = 'user-input/';
      $download_loc = $uploads_dir . basename($_FILES['query']['name']);
    
      
      if (move_uploaded_file($_FILES['query']['tmp_name'], $download_loc)) {
        //echo "File is valid, and was successfully downloaded.\n";
      } else {
        echo "File download failed\n";
      }
      
      /*
      echo 'Here is some more debugging info:';
      print_r($_FILES);
      */
      $download_loc_escaped = escapeshellarg($download_loc); //handle file names with spaces
      $results = json_decode(shell_exec("python process_music.py " .$download_loc_escaped = escapeshellarg($download_loc)), true); 
   
      $col_names = array("Song", "Composer (s)");
      $col_indices = array(0, 1);
      //display the results in a table
      echo "<table class='ml-2 mt-2 border-2 border-black shadow-lg' style='border: border-collapse: collapse; margin-left: auto; margin-right: auto; width: 50%;'>\n"; 
      echo "<tr>";
      foreach($col_names as $name) {
        echo "<th style='border: 1px solid black; padding: 8px;'>" . $name . "</th>";
      }
      echo "</tr>\n";

      foreach($results as $result) {
        echo "<tr>";
          foreach($col_indices as $i) {
            echo "<td style='border: 1px solid black; padding: 8px;'>" . $result[$i] . "</td>";
          }
        echo "</tr>\n";
      }
          
      echo "</table>\n";

  
      //remove the file when done to save space
      if (!unlink($download_loc)) { 
        //echo ("$download_loc cannot be deleted due to an error"); sometimes shows for no reason?
      } else { 
        //echo ("$download_loc has been deleted"); 
      }
  
  } catch (RuntimeException $e) {
  
      echo $e->getMessage();
  
  }
      
  ?>
</body>
