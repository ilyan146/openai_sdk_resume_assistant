import "react"
import {Outlet, Link, Navigate} from "react-router-dom";

export function Layout() {
    return <div className="app-layout">
        <header className="app-header">
            <div className="header-content">
                <h1>Chat Interface</h1>
                <nav>
                    <Link to="/">Home</Link>
                    <Link to="/history">History</Link>
                </nav>
            </div>
        </header>
        <main className="app-main">
            {/*<Navigate to="/info" replace/>*/}
            <Outlet />

        </main>
    </div>
}