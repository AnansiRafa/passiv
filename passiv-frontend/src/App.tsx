import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import ContentFeed from "./components/ContentFeed";
import ContentDetail from "./components/ContentDetail";

function App(): JSX.Element {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<ContentFeed />} />
        <Route path="/content/:id" element={<ContentDetail />} />
      </Routes>
    </Router>
  );
}

export default App;
