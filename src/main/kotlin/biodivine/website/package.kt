package biodivine.website

import kotlinx.html.*
import kotlinx.html.dom.createHTMLDocument
import kotlinx.html.dom.serialize

fun makeBiodivinePage(path: String, makeContent: DIV.() -> Unit): String = createHTMLDocument().html {
    head {
        // Include material icons font
        link(   rel = ARel.stylesheet,
                href = "https://fonts.googleapis.com/icon?family=Material+Icons"
        )
        // Include material design components
        link(   rel = ARel.stylesheet,
                href = "https://unpkg.com/material-components-web@latest/dist/material-components-web.min.css"
        )
        script( type = AType.textJavaScript,
                src = "https://unpkg.com/material-components-web@latest/dist/material-components-web.min.js"
        ) {}
        style(type = AType.textCss) {
            unsafe {
                +"body { margin: 0; }"
                +".bio { color: green; font-weight: bold; }"
                //TODO +":root { --mdc-theme-primary: #ff0000; }"
            }
        }
    }
    body {

        div {
            makeTopBar(path)
            makeContent()
        }

        // Try to automatically initialize material design components
        script(type = AType.textJavaScript) {
            unsafe {
                +"window.mdc.autoInit();"
            }
        }
    }
}.serialize()

fun DIV.makeTopBar(path: String) {
    header(classes = "mdc-top-app-bar") {
        div(classes = "mdc-top-app-bar__row") {
            section(classes = "mdc-top-app-bar__section mdc-top-app-bar__section--align-start") {
                a(href = "#", classes = "material-icons mdc-top-app-bar__navigation-icon") { +"menu" }
                span(classes = "mdc-top-app-bar__title") { bioDivine() }
            }
            section(classes = "mdc-top-app-bar__section mdc-top-app-bar__section--align-end mdc-top-app-bar__section--fit-content") {
                div(classes = "mdc-tab-bar") {
                    div(classes = "mdc-tab-scroller") {
                        div(classes = "mdc-tab-scroller__scroll-area") {
                            div(classes = "mdc-tab-scroller__scroll-content") {
                                button(classes = "mdc-tab mdc-tab--active mdc-tab--min-width") {
                                    span(classes = "mdc-tab__content") {
                                        span(classes = "mdc-tab__text-label") {
                                            attributes["style"] = "color: white;"
                                            +"Tools"
                                        }
                                    }
                                    span(classes = "mdc-tab-indicator mdc-tab-indicator--active") {
                                        span(classes = "mdc-tab-indicator__content mdc-tab-indicator__content--underline") {
                                            attributes["style"] = "background-color: white;"
                                        }
                                    }
                                    span(classes = "mdc-tab__ripple")
                                }

                                button(classes = "mdc-tab") {
                                    span(classes = "mdc-tab__content") {
                                        span(classes = "mdc-tab__text-label") {
                                            attributes["style"] = "color: white;"
                                            +"Notebooks"
                                        }
                                    }
                                    span(classes = "mdc-tab-indicator") {
                                        span(classes = "mdc-tab-indicator__content mdc-tab-indicator__content--underline") {
                                            attributes["style"] = "background-color: white;"
                                        }
                                    }
                                    span(classes = "mdc-tab__ripple")
                                }

                                button(classes = "mdc-tab") {
                                    span(classes = "mdc-tab__content") {
                                        span(classes = "mdc-tab__text-label") {
                                            attributes["style"] = "color: white;"
                                            +"Libraries"
                                        }
                                    }
                                    span(classes = "mdc-tab-indicator") {
                                        span(classes = "mdc-tab-indicator__content mdc-tab-indicator__content--underline")
                                    }
                                    span(classes = "mdc-tab__ripple")
                                }

                                button(classes = "mdc-tab") {
                                    span(classes = "mdc-tab__content") {
                                        span(classes = "mdc-tab__text-label") {
                                            attributes["style"] = "color: white;"
                                            +"Developers"
                                        }
                                    }
                                    span(classes = "mdc-tab-indicator") {
                                        span(classes = "mdc-tab-indicator__content mdc-tab-indicator__content--underline")
                                    }
                                    span(classes = "mdc-tab__ripple")
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

fun FlowOrPhrasingContent.bioDivine() {
    span(classes = "bio") { +"Bio" }
    +"Divine"
}