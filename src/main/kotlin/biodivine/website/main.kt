package biodivine.website

import java.io.File

fun main(args: Array<String>) {

    val outFolder = File("out/website")
    outFolder.mkdirs()

    val homepage = makeBiodivinePage("/") {
        +"Some content"
    }

    File(outFolder, "index.html").writeText(homepage)
}