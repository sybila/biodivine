package biodivine.homepage

import kotlinx.html.*
import kotlinx.html.dom.createHTMLDocument
import kotlinx.html.dom.serialize
import kotlinx.html.stream.createHTML
import org.commonmark.renderer.html.HtmlRenderer
import java.io.File
import org.commonmark.parser.Parser as Markdown

/**
 * Web page is a single static html resource which serves HTML at specified [path].
 *
 * It can provide several sub-pages which will reside at their respective sub-paths.
 */
interface WebPage {

    val parent: WebPage?
    val children: List<WebPage>

    val path: String

    fun makeHTML(): String

    fun makeSite(out: File) {
        val pathDir = File(out, path)
        if (!pathDir.exists() && !pathDir.mkdirs()) error("Cannot create directory ${pathDir.absolutePath}")
        val siteFile = File(pathDir, "index.html")
        siteFile.writeText(makeHTML())
        children.forEach {
            it.makeSite(pathDir)
        }
    }

}

abstract class BioDivinePage(
        override val path: String, override val parent: WebPage?
) : WebPage {

    abstract fun BODY.makeBody(): Unit

    override fun makeHTML(): String = createHTMLDocument().html {
        head {
            link(rel = ARel.stylesheet, href = "bundle.css")
        }
        body {
            makeBody()
            script(type = AType.textJavaScript, src = "bundle.js") {}
        }
    }.serialize()

}

fun main(args: Array<String>) {
    val outFolder = File("out/html")
    val inFolder = File("content")

    val markdown = Markdown.builder().build()
    val renderer = HtmlRenderer.builder().build()

    val homepage = object : BioDivinePage("test", null) {

        override val children: List<WebPage> = emptyList()

        override fun BODY.makeBody() = div {
            h1 { +"This is a title in the kotlin code" }
            this.unsafe {
                +renderer.render(markdown.parse(File(inFolder, "$path.md").readText()))
            }
        }
    }

    homepage.makeSite(outFolder)
}

