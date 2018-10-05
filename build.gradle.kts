plugins {
	application
	kotlin("jvm") version "1.2.71"
}

application {
	mainClassName = "biodivine.homepage.MainKt"
}

repositories {
	jcenter()
}

dependencies {
	implementation(kotlin("stdlib"))
	implementation("org.jetbrains.kotlinx", "kotlinx-html-jvm", "0.6.11")
	implementation("com.atlassian.commonmark", "commonmark", "0.11.0")
}
