plugins {
	application
	kotlin("jvm") version "1.3.10"
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
