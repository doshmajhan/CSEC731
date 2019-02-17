<?php
use PHPUnit\Framework\TestCase;
include("webapp.php");

class WebAppTest extends TestCase
{

    public function testBasic()
    {
        $name = "test.txt";
        $contents = "foobar";
        $this->assertTrue(main("create", $name, $contents));

        $this->expectOutputString("foobar");
        main("view", $name, $contents);

        $this->assertTrue(main("del", $name, $contents));
    }

    public function testBashInjection()
    {
        $name = "test.txt; nc -nlvp 8000";
        $contents = "foobar";
        $this->assertTrue(main("create", $name, $contents));


        $this->assertTrue(main("del", $name, $contents));
    }

    public function testTraversal()
    {
        $name = "../../../../../../../etc/passwd";
        $contents = "foobar";
        $this->assertFalse(main("view", $name, $contents));
    }
}

?>