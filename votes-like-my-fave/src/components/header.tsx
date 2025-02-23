
export function Header() {
  return (
    <header className="bg-blue-900 text-white py-4 shadow-md">
      <div className="container mx-auto flex justify-between items-center px-4">
        <h1 className="text-xl font-bold flex items-center">
          <span className="mr-2">🇺🇸</span> Who  Votes Like My Fave?
        </h1>
        {/* <nav>
          <ul className="flex space-x-4">
            <li>
              <a href="#" className="text-white hover:underline">
                Home
              </a>
            </li>
            <li>
              <a href="#" className="text-white hover:underline">
                Status
              </a>
            </li>
            <li>
              <a href="#" className="text-white hover:underline">
                About
              </a>
            </li>
          </ul>
        </nav> */}
      </div>
    </header>
  );
};