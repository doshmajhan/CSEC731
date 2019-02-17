<?php
    // Small web app to write/read/delete files in /tmp/webapp
    
    // Get parameters
    $method = $_GET['method'];
    $fname = $_GET['name'];
    $contents = $_GET['contents'];
    
    function main($method, $fname, $contents)
    {
        $directory = "/tmp/webapp/";
        if (!is_dir($directory))
        {
            mkdir($directory, 0777, true);
        }

        // Santize
        $fname = escapeshellcmd($fname);
        $fname = basename($fname);
        $filepath = $directory . $fname;
        //echo nl2br($fname . "\n");
        //echo nl2br($filepath . "\n");

        if ($filepath === false || strpos($filepath, $directory) !== 0)
        {
            http_response_code(400);
            echo "Can only write/read files in /tmp/webapp";
        } 
        else 
        {
            return execute_method($method, $filepath, $contents);
        }
    }

    // Determine method to execute
    function execute_method($method, $filepath, $contents)
    {
        if (strcmp($method, 'create') == 0)
        {
            return create_file($filepath, $contents);
        } 
        elseif (strcmp($method, 'del') == 0)
        {
            return delete_file($filepath);
        } 
        elseif (strcmp($method, 'view') == 0)
        {
            return view_file($filepath);
        }
        else
        {
            // return error
            http_response_code(400);
            echo "Method not supported";
            return false;
        }
    }


    function create_file($name, $contents)
    {
        $file = fopen($name, "w") or die("Unable to open file!");
        fwrite($file, $contents);
        //echo "File Created";
        fclose($file);
        return true;
    }

    function delete_file($name)
    {
        unlink($name);
        //echo "File Deleted";
        return true;
    }

    function view_file($name)
    {
        try 
        {
            $contents = file_get_contents($name) or die("Unable to open file!");
            echo $contents;
        }
        catch (Exception $e)
        {
            echo "Can't access file";
            return false;
        }
        
        return true;
    }
?>