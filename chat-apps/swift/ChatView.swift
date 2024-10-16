import SwiftUI

struct Message: Identifiable {
    let id = UUID()
    var text: String
    let isUser: Bool
}

class ChatViewModel: ObservableObject {
    @Published var messages: [Message] = []
    @Published var userInput: String = ""
    @Published var isLoading = false
    
    let apiKey: String =  "Enter_your_API_key_here"
    let baseUrl: String = "https://api.centml.com/openai/v1/chat/completions"
    let modelName: String = "meta-llama/Meta-Llama-3-8B-Instruct"
    
    // Function to send a message and receive a response via streaming
    func sendMessage() {
        let userMessage = userInput.trimmingCharacters(in: .whitespacesAndNewlines)
        if userMessage.isEmpty { return }
        
        // Add user's message to the conversation
        messages.append(Message(text: userMessage, isUser: true))
        userInput = ""
        
        // Start streaming assistant's response
        fetchStreamingResponse(userMessage: userMessage)
    }
    
    // Function to make a POST request with streaming enabled
    private func fetchStreamingResponse(userMessage: String) {
        isLoading = true
        guard let url = URL(string: baseUrl) else { return }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.addValue("Bearer \(apiKey)", forHTTPHeaderField: "Authorization")
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let body: [String: Any] = [
            "model": modelName,
            "messages": [
                ["role": "system", "content": "You are helpful"],
                ["role": "user", "content": userMessage]
            ],
            "max_tokens": 2000,
            "n": 1,
            "stream": true,
            "temperature": 0.7,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "stop": []
        ]
        
        request.httpBody = try? JSONSerialization.data(withJSONObject: body, options: [])
        
        let sessionConfiguration = URLSessionConfiguration.default
        let streamingDelegate = StreamingDelegate(viewModel: self)
        let session = URLSession(configuration: sessionConfiguration, delegate: streamingDelegate, delegateQueue: nil)
        
        let task = session.dataTask(with: request)
        task.resume()
    }
}

// StreamingDelegate to handle streaming response from the API
class StreamingDelegate: NSObject, URLSessionDataDelegate {
    @ObservedObject var viewModel: ChatViewModel
    
    init(viewModel: ChatViewModel) {
        self.viewModel = viewModel
    }
    
    func urlSession(_ session: URLSession, dataTask: URLSessionDataTask, didReceive data: Data) {
        if let responseText = String(data: data, encoding: .utf8) {
            let lines = responseText.split(separator: "\n")
            for line in lines {
                if line.hasPrefix("data:") {
                    let jsonData = line.dropFirst(5).trimmingCharacters(in: .whitespaces)
                    if jsonData != "[DONE]" {
                        if let data = jsonData.data(using: .utf8),
                           let jsonResponse = try? JSONSerialization.jsonObject(with: data, options: []) as? [String: Any],
                           let choices = jsonResponse["choices"] as? [[String: Any]],
                           let delta = choices.first?["delta"] as? [String: String],
                           let content = delta["content"] {
                            
                            DispatchQueue.main.async {
                                if let lastMessage = self.viewModel.messages.last, !lastMessage.isUser {
                                    self.viewModel.messages[self.viewModel.messages.count - 1].text += content
                                } else {
                                    self.viewModel.messages.append(Message(text: content, isUser: false))
                                }
                            }
                        }
                    } else {
                        DispatchQueue.main.async {
                            self.viewModel.isLoading = false
                        }
                    }
                }
            }
        }
    }
    
    func urlSession(_ session: URLSession, task: URLSessionTask, didCompleteWithError error: Error?) {
        DispatchQueue.main.async {
            if let error = error {
                print("Error: \(error.localizedDescription)")
            }
            self.viewModel.isLoading = false
        }
    }
}

struct ChatView: View {
    @ObservedObject var viewModel = ChatViewModel()
    
    var body: some View {
        VStack {
            ScrollView {
                VStack(alignment: .leading, spacing: 8) {
                    ForEach(viewModel.messages) { message in
                        HStack {
                            if message.isUser {
                                Spacer()
                                Text(message.text)
                                    .padding()
                                    .background(Color.blue)
                                    .foregroundColor(.white)
                                    .cornerRadius(10)
                            } else {
                                Text(message.text)
                                    .padding()
                                    .background(Color.gray.opacity(0.2))
                                    .cornerRadius(10)
                                Spacer()
                            }
                        }
                    }
                }
            }
            .padding()
            
            // Input and Send Button
            HStack {
                TextField("Enter your message here", text: $viewModel.userInput)
                    .padding()
                    .background(Color.gray.opacity(0.2))
                    .cornerRadius(10)
                
                Button(action: {
                    viewModel.sendMessage()
                }) {
                    if viewModel.isLoading {
                        ProgressView()
                    } else {
                        Image(systemName: "paperplane.fill")
                            .font(.system(size: 24))
                            .padding()
                    }
                }
                .disabled(viewModel.userInput.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty)
            }
            .padding()
        }
        .navigationTitle("Chat with Meta-Llama")
    }
}
