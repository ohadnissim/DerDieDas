import UIKit
import Capacitor

class SceneDelegate: UIResponder, UIWindowSceneDelegate {
    var window: UIWindow?

    func scene(_ scene: UIScene, willConnectTo session: UISceneSession, options connectionOptions: UIScene.ConnectionOptions) {
        guard let windowScene = scene as? UIWindowScene else { return }

        window = UIWindow(windowScene: windowScene)
        window?.rootViewController = MainViewController()
        window?.makeKeyAndVisible()

        SceneDelegateProxy.shared.scene(scene, willConnectTo: session, options: connectionOptions)
    }

    func scene(_ scene: UIScene, openURLContexts URLContexts: Set<UIOpenURLContext>) {
        SceneDelegateProxy.shared.scene(scene, openURLContexts: URLContexts)
    }

    func scene(_ scene: UIScene, continue userActivity: NSUserActivity) {
        SceneDelegateProxy.shared.scene(scene, continue: userActivity)
    }
}

// The app's web storage can be emptied by iOS (her islands and stickers were lost after an app update),
// so the page also keeps its save here, in the app's own settings, which an update never touches.
class MainViewController: CAPBridgeViewController {
    override func capacitorDidLoad() {
        bridge?.registerPluginInstance(SaveStorePlugin())
    }
}

@objc(SaveStorePlugin)
public class SaveStorePlugin: CAPPlugin, CAPBridgedPlugin {
    public let identifier = "SaveStorePlugin"
    public let jsName = "SaveStore"
    public let pluginMethods: [CAPPluginMethod] = [
        CAPPluginMethod(name: "get", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "set", returnType: CAPPluginReturnPromise)
    ]

    private func storeKey(_ call: CAPPluginCall) -> String {
        return "web." + (call.getString("key") ?? "save")
    }

    @objc func get(_ call: CAPPluginCall) {
        if let value = UserDefaults.standard.string(forKey: storeKey(call)) {
            call.resolve(["value": value])
        } else {
            call.resolve()
        }
    }

    @objc func set(_ call: CAPPluginCall) {
        guard let value = call.getString("value") else {
            call.reject("no value")
            return
        }
        UserDefaults.standard.set(value, forKey: storeKey(call))
        call.resolve()
    }
}
