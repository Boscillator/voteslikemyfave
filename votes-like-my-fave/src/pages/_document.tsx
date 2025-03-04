import { Html, Head, Main, NextScript } from "next/document";
import { Header } from "@/components/header";
import Footer from "@/components/footer";

export default function Document() {
  return (
    <Html lang="en">
      <Head />
      <body className="antialiased bg-gray-100 flex flex-col min-h-screen w-full">
        <Header />
        <main className="flex-grow mb-10 p-4">
          <Main />
        </main>
        <NextScript />
        <Footer />
      </body>
    </Html>
  );
}
