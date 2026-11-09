#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_http::init()) // lets the page talk to Ollama on this machine
        .run(tauri::generate_context!())
        .expect("Jarvis konnte nicht starten");
}
